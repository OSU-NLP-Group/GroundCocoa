import subprocess

scripts = ["scrape_flight_data.py", "requirements_generator.py", "llm_q_generator.py", "construct_final_dataset.py"]

for script in scripts:
    subprocess.run(["python", script])
