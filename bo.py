import optuna
import subprocess
import os
import uuid
import shutil
import random

# === Évaluation factice (à remplacer par CLIP ou autre) ===
def dummy_evaluate(output_dir):
    return random.uniform(0.0, 1.0)  # simule un score aléatoire

# === Fonction objectif Optuna ===
def objective(trial):
    # Hyperparamètres à tester
    batch_size = trial.suggest_categorical("train_batch_size", [8, 16])
    lr = trial.suggest_float("learning_rate", 1e-5, 2e-4, log=True)
    resolution = trial.suggest_categorical("resolution", [512, 768])
    grad_steps = trial.suggest_categorical("gradient_accumulation_steps", [1, 2])
    scheduler = trial.suggest_categorical("lr_scheduler", ["linear", "cosine"])
    train_text_encoder = trial.suggest_categorical("train_text_encoder", [True, False])
    prediction_type = trial.suggest_categorical("prediction_type", ["epsilon", "v_prediction"])
    snr_gamma = trial.suggest_float("snr_gamma", 1.0, 5.0)

    # Dossier de sortie unique
    run_id = str(uuid.uuid4())[:8]
    output_dir = f"optuna_runs/sdxl_tryon_{run_id}"

    # Commande d'entraînement
    cmd = [
        "accelerate", "launch", "train_text_to_image_lora_sdxl.py",
        "--pretrained_model_name_or_path=stabilityai/stable-diffusion-xl-base-1.0",
        "--pretrained_vae_model_name_or_path=madebyollin/sdxl-vae-fp16-fix",
        "--train_data_dir=../../../../VITON-HD-512/train_images/",
        "--caption_column=text",
        "--validation_prompt=A portrait of a pregnant black woman in her thirties, plain background.",
        "--output_dir", output_dir,
        "--mixed_precision=fp16",
        "--num_validation_images=1",
        "--dataloader_num_workers=8",
        "--seed=1337",
        "--train_batch_size", str(batch_size),
        "--learning_rate", str(lr),
        "--resolution", str(resolution),
        "--gradient_accumulation_steps", str(grad_steps),
        "--lr_scheduler", scheduler,
        "--prediction_type", prediction_type,
        "--snr_gamma", str(snr_gamma),
        "--enable_optuna_pruning"
    ]
    if train_text_encoder:
        cmd.append("--train_text_encoder")

    try:
        print(f"🔁 Lancement de l'entraînement pour les params : {trial.params}")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[❌ Échec] L'entraînement a échoué pour cette config.")
        return 0.0  # Score nul si erreur

    # Évaluation automatique (ou manuelle)
    score = dummy_evaluate(output_dir)

    # Optionnel : nettoyage (à commenter si tu veux garder les runs)
    shutil.rmtree(output_dir, ignore_errors=True)

    return score  # Plus haut = mieux

# === Exécution de l’optimisation ===
if __name__ == "__main__":
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=10)

    # Résumé
    print("🏆 Meilleurs hyperparamètres trouvés :")
    print(study.best_params)

    # Visualisation
    try:
        import optuna.visualization as vis
        vis.plot_optimization_history(study).show()
        vis.plot_param_importances(study).show()
        vis.plot_parallel_coordinate(study).show()
    except Exception as e:
        print("⚠️ Impossible d'afficher les plots automatiquement.")
