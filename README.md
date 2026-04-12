# 🫀 Heart Disease Prediction using Deep Learning with Multi-Class Classification

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Development-red)](https://github.com/)

A clinical decision support tool designed for healthcare professionals. By leveraging deep learning and ensemble machine learning models, the system categorizes patient risk levels into **Low**, **Medium**, or **High** categories based on clinical parameters.

---

## 🚀 Key Features

* **Multi-Model Engine:** Utilizes a Feedforward Artificial Neural Network (ANN) as the primary engine, with Random Forest and Logistic Regression as comparative benchmarks.
* **Tri-Level Risk Assessment:** Move beyond binary "yes/no" predictions with multi-class classification.
* **Clinical Dashboard:** A clean, web-based GUI for rapid data entry and instant probability scoring.
* **Automated Preprocessing:** Built-in pipeline for data normalization, categorical encoding, and handling of missing clinical values.
* **⚠️ [PENDING] Historical Visualization:** Future updates will include interactive charts showing health risk trends over time for individual patients.
* **⚠️ [PENDING] Secure Data Persistence:** Database integration for patient history and report generation is currently in the development roadmap.
---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.8 or higher
* Pip (Python Package Manager)

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/drnafees/Heart-Disease-Prediction.git
   cd Heart-Disease-Prediction
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Train the models:**
   ```bash
   python train_models.py
   ```
4. **Run the application:**
   ```bash
   python app.py
   ```
---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Disclaimer:** *This system is intended for research and educational purposes only and is designed to serve as a decision-support adjunct for qualified healthcare professionals. It does not provide medical advice, diagnosis, or treatment. All clinical decisions should be made by a licensed practitioner based on their independent professional judgment, comprehensive patient examination, and established clinical protocols. Use of this software does not establish a provider-patient relationship. Use of this system is at the user's own risk.*
