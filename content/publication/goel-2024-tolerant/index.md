---
title: Tolerant Algorithms for Learning with Arbitrary Covariate Shift
date: '2024-12-07'
draft: false
publishDate: '2024-08-12T19:47:13.850512Z'
authors:
- Surbhi Goel
- Abhishek Shetty
- admin
- Arsen Vasilyan
publication_types:
- 'paper-conference'
abstract: 'We study the problem of learning under arbitrary distribution shift, where the learner is trained on a labeled set from one distribution but evaluated on a different, potentially adversarially generated test distribution. We focus on two frameworks: PQ learning [GKKM20], allowing abstention on adversarially generated parts of the test distribution, and TDS learning [KSV24b], permitting abstention on the entire test distribution if distribution shift is detected. All prior known algorithms either rely on learning primitives that are computationally hard even for simple function classes, or end up abstaining entirely even in the presence of a tiny amount of distribution shift.

We address both these challenges for natural function classes, including intersections of halfspaces and decision trees, and standard training distributions, including Gaussians. For PQ learning, we give efficient learning algorithms, while for TDS learning, our algorithms can tolerate moderate amounts of distribution shift. At the core of our approach is an improved analysis of spectral outlier-removal techniques from learning with nasty noise. Our analysis can (1) handle arbitrarily large fraction of outliers, which is crucial for handling arbitrary distribution shifts, and (2) obtain stronger bounds on polynomial moments of the distribution after outlier removal, yielding new insights into polynomial regression under distribution shifts. Lastly, our techniques lead to novel results for tolerant testable learning [RV23], and learning with nasty noise.'
featured: true
publication: '**NeurIPS 2024** <span style="font-size:15px;"><i class="fa-solid fa-star"></i></span> ***Spotlight***'
url_pdf: https://arxiv.org/pdf/2406.02742
links:
- name: URL
  url: https://arxiv.org/abs/2406.02742
---

