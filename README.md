# VoSQL
VoSQL: An Easy to Use Database Query Engine

## Components

### Written from scratch

- Front-end and UI: `/front`
- Database detection deploy API: `/db_infer`
- Database detection model and training details: `/db_detect_train`

### Modified open-source code

- IRNet modified ([original source](https://github.com/microsoft/IRNet)): `/IRNet_deploy`

    - Deploy API Server: `/IRNet_deploy/e2e.ipynb`

## References

[1] Yu, Tao, et al. "Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task." Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. 2018.

[2] Guo, Jiaqi, et al. "Towards Complex Text-to-SQL in Cross-Domain Database with Intermediate Representation." arXiv preprint arXiv:1905.08205 (2019).

[3] Devlin, Jacob, et al. "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers). 2019.