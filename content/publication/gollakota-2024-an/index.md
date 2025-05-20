---
title: An Efficient Tester-Learner for Halfspaces
date: '2024-01-01'
draft: false
publishDate: '2024-08-12T19:48:58.474619Z'
authors:
- Aravind Gollakota
- Adam Klivans
- admin
- Arsen Vasilyan
publication_types:
- 'paper-conference'
abstract: 'We give the first efficient algorithm for learning halfspaces in the testable learning model recently defined by Rubinfeld and Vasilyan [2022]. In this model, a learner certifies that the accuracy of its output hypothesis is near optimal whenever the training set passes an associated test, and training sets drawn from some target distribution must pass the test. This model is more challenging than distribution-specific agnostic or Massart noise models where the learner is allowed to fail arbitrarily if the distributional assumption does not hold. We consider the setting where the target distribution is the standard Gaussian in $d$ dimensions and the label noise is either Massart or adversarial (agnostic). For Massart noise, our tester-learner runs in polynomial time and outputs a hypothesis with (information-theoretically optimal) error $\mathrm{opt}+\epsilon$ (and extends to any fixed strongly log-concave target distribution). For adversarial noise, our tester-learner obtains error $O(\mathrm{opt})+\epsilon$ in polynomial time. Prior work on testable learning ignores the labels in the training set and checks that the empirical moments of the covariates are close to the moments of the base distribution. Here we develop new tests of independent interest that make critical use of the labels and combine them with the moment-matching approach of Gollakota et al. [2022]. This enables us to implement a testable variant of the algorithm of Diakonikolas et al. [2020a, 2020b] for learning noisy halfspaces using nonconvex SGD.'
featured: true
publication: '**ICLR 2024**'
url_pdf: https://openreview.net/pdf?id=z6n1fKMMC1
links:
- name: URL
  url: https://openreview.net/forum?id=z6n1fKMMC1
---

