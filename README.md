# Advanced Deepfake Detection  
*Sequential Inception-ResNet-v2 Pipeline with MTCNN Pre-processing*

**Authors:** Anjali Kaushik, Dhyey Nilesh Doshi, Sandip Mal & Lokesh Malviya  
**Affiliation:** Vellore Institute of Technology, Bhopal
**Conference:** ICCIS'23 by the Soft-Computing Society of India, National Institute of Technology, Jaipur
**Paper:** [Springer LNNS Vol. 967, “Advanced Deepfake Detection”](https://link.springer.com/chapter/10.1007/978-981-97-2053-8_11)

---

## ✨ Project Overview
This repository accompanies our research on **automatic deep-fake video detection**.  
We combine **MTCNN face extraction** with a **Sequential CNN headed by Inception-ResNet-v2** and custom dense layers to classify real vs fake frames, then aggregate scores across each clip.

Core pipeline stages:

1. **Face Extraction (MTCNN)** – robust to scale, occlusion, & pose.  
2. **Frame-level Feature Learning** – 299×299 crops through frozen *Inception-ResNet-v2*.  
3. **Fine-Tuned Classification Head** – GAP → Dense (128→64→32) → Dropout 0.5 → Dense 2-way Softmax.  
4. **Video Decision** – majority vote or probability mean across sampled frames.

Extensive experiments on **23 k+ DFDC videos** yield **91.41 % validation accuracy**, surpassing plain CNN (84.9 %) and Xception-Net (85.5 %). :contentReference[oaicite:2]{index=2}&#8203;:contentReference[oaicite:3]{index=3}

---

## 🎯 Key Features
| Module | Highlights |
|--------|-----------|
| **MTCNN Pre-processing** | High recall on very small & obstructed faces |
| **Transfer-Learning Backbone** | Inception-ResNet-v2, 164 layers, ImageNet weights |
| **Lightweight Head** | < 5 M trainable params; mitigates over-fitting with dropout |
| **Quality-Agnostic** | Performs on both high & heavily compressed DFDC clips |
| **Metrics Suite** | ROC, sensitivity 96.5 %, specificity 92.8 % reported in paper |

---

## Citation
@inproceedings{kaushik2024deepfake,
  author    = {Anjali Kaushik and Dhyey N. Doshi and Sandip Mal and Lokesh Malviya},
  title     = {Advanced Deepfake Detection Using Inception-ResNet-v2},
  booktitle = {Proc. Nat. IT Conf.},
  year      = {2024},
  series    = {Lecture Notes in Networks and Systems},
  volume    = {967}
}

