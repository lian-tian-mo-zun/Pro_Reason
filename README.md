# ProReason 🤖
Official Code for the Paper "ProReason: Multi-Modal Proactive Reasoning with Decoupled Eyesight and Wisdom"
---
✨We introduce **ProReason**, a novel multi-modal reasoning framework featuring multi-run proactive perception and decoupled vision-reasoning capabilities. Briefly, given a multi-modal question, ProReason iterates **pro**active information collection and **reason**ing until the answer can be concluded with necessary and sufficient visual descriptions.

🤖ProReason showcases the remarkable feasibility of integrating LLMs for multi-modal reasoning with dramatically improved performance, highlighting the great potential for LLM-assisted LVLM reasoning in future research.

A more thorough discussion of our work can be found in our [paper](https://arxiv.org/abs/2410.14138).

### 🧠 Method Description
---
<p align="center">
  <img src=images/ProReason.jpg />
</p>

**ProReason** can be divided into three stages: **Action**, **Judgment**, and **Summary**, with each involving different agents.
In the Action stage, a Dispatcher selectively engages a Vision Expert to capture additional visual information, or a Reasoning Expert to derive more insights. 
Unlike passive methods, all three agents operate based on the given question and current descriptions, effectively avoiding information redundancy or insufficiency.
Subsequently, a Referee in the Judgment stage evaluates the sufficiency of known information,
deciding whether to return to the Action stage or proceed to the Summary stage, where all information is consolidated for a Summarizer to generate the final answer.
Notably, the disentangled vision-reasoning does not require vision-irrelevant roles (i.e., Reasoning Expert, Referee, and Summarizer) to be performed by LVLMs, enabling the seamless integration of existing LLMs with proven strong reasoning abilities, thereby addressing the limitations of LVLMs.

### 💻 Exploring ProReason
---
We present [HallusionBench](https://github.com/tianyi-lab/HallusionBench/tree/main?tab=readme-ov-file) as a case study to demonstrate the performance of ProReason, using GPT-4o mini as the default model.

#### Data Preparation
1.Download the [text data](https://github.com/tianyi-lab/HallusionBench/blob/main/HallusionBench.json) of HallusionBench and place the `HallusionBench.json` in the `ProReason_HallusionBench`.

2.Download the [image data](https://drive.google.com/file/d/1eeO1i0G9BSZTE1yd5XeFwmrbe1hwyf_0/view?usp=sharing) of HallusionBench, and after extracting, place the `VD` and `VS` folders in the `ProReason_HallusionBench`.

#### Inference
Run the following command to enter the ProReason_HallusionBench folder and execute ProReason_HallusionBench_test.py.
```bash
cd ./ProReason_main/ProReason_HallusionBench
python ProReason_HallusionBench_test.py
```
The inference results of ProReason will be stored in `ProReason_HallusionBench.json`.

#### Evaluation
Run the following command to evaluate ProReason's performance on HallusionBench.
```bash
python evaluation.py
```

### 📝 Citation
---
If you found our work useful, please consider starring and citing. Thank you!
```latex
@article{zhou2024proreason,
  title={ProReason: Multi-Modal Proactive Reasoning with Decoupled Eyesight and Wisdom},
  author={Zhou, Jingqi and Wang, Sheng and Dong, Jingwei and Li, Lei and Gao, Jiahui and Kong, Lingpeng and Wu, Chuan},
  journal={arXiv preprint arXiv:2410.14138},
  year={2024}
}
```
