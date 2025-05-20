---
title: 'Learning Neural Networks with Distribution Shift: Efficiently Certifiable Guarantees'
date: '2025-04-10'
draft: false
publishDate: '2024-10-12T19:47:11.824636Z'
authors:
- Gautam Chandrasekaran
- Adam Klivans
- Lin Lin Lee
- admin
publication_types:
- 'paper-conference'
abstract: 'We give the first provably efficient algorithms for learning neural networks with distribution shift. We work in the Testable Learning with Distribution Shift framework (TDS learning) of Klivans et al. (2024), where the learner receives labeled examples from a training distribution and unlabeled examples from a test distribution and must either output a hypothesis with low test error or reject if distribution shift is detected. No assumptions are made on the test distribution. All prior work in TDS learning focuses on classification, while here we must handle the setting of nonconvex regression. Our results apply to real-valued networks with arbitrary Lipschitz activations and work whenever the training distribution has strictly sub-exponential tails. For training distributions that are bounded and hypercontractive, we give a fully polynomial-time algorithm for TDS learning one hidden-layer networks with sigmoid activations. We achieve this by importing classical kernel methods into the TDS framework using data-dependent feature maps and a type of kernel matrix that couples samples from both train and test distributions.'
featured: true
publication: '**ICLR 2025**'
url_pdf: 'https://arxiv.org/pdf/2502.16021'
links:
 - name: URL
   url: 'https://arxiv.org/abs/2502.16021'
---