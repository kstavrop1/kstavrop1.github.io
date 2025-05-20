---
title: Testing Noise Assumptions of Learning Algorithms
date: '2025-01-01'
draft: false
publishDate: '2024-08-12T19:48:58.474619Z'
authors:
- Surbhi Goel
- Adam Klivans
- admin
- Arsen Vasilyan
publication_types:
- 'paper-conference'
abstract: "We pose a fundamental question in computational learning theory: can we efficiently test whether a training set satisfies the assumptions of a given noise model? This question has remained unaddressed despite decades of research on learning in the presence of noise. In this work, we show that this task is tractable and present the first efficient algorithm to test various noise assumptions on the training data.
To model this question, we extend the recently proposed testable learning framework of Rubinfeld and Vasilyan (2023) and require a learner to run an associated test that satisfies the following two conditions: (1) whenever the test accepts, the learner outputs a classifier along with a certificate of optimality, and (2) the test must pass for any dataset drawn according to a specified modeling assumption on both the marginal distribution and the noise model. We then consider the problem of learning halfspaces over Gaussian marginals with Massart noise (where each label can be flipped with probability less than $1/2$ depending on the input features), and give a fully-polynomial time testable learning algorithm.
We also show a separation between the classical setting of learning in the presence of structured noise and testable learning. In fact, for the simple case of random classification noise (where each label is flipped with fixed probability $1/2$), we show that testable learning requires super-polynomial time while classical learning is trivial."
featured: false
publication: '*Under review*'
url_pdf: https://arxiv.org/pdf/2501.09189
links:
- name: URL
  url: https://arxiv.org/abs/2501.09189
---

