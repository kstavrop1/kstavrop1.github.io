---
title: 'Learning Intersections of Halfspaces with Distribution Shift: Improved Algorithms
  and SQ Lower Bounds'
date: '2024-06-29'
draft: false
publishDate: '2024-08-12T19:48:58.022344Z'
authors:
- Adam Klivans
- admin
- Arsen Vasilyan
publication_types:
- 'paper-conference'
abstract: '  Recent work of Klivans, Stavropoulos, and Vasilyan initiated the study
  of testable learning with distribution shift (TDS learning), where a learner is
  given labeled samples from training distribution $\mathcal{D}$, unlabeled samples from
  test distribution $\mathcal{D’}$, and the goal is to output a classifier with low error
  on $\mathcal{D’}$ whenever the training samples pass a corresponding test.  Their model
  deviates from all prior work in that no assumptions are made on $\mathcal{D’}$.  Instead,
  the test must accept (with high probability) when the marginals of the training
  and test distributions are equal.  Here we focus on the fundamental case of intersections
  of halfspaces with respect to Gaussian training distributions and prove a variety
  of new upper bounds including a $2^{(k/\epsilon)^O(1)} \mathsf{poly}(d)$-time algorithm for
  TDS learning intersections of $k$ homogeneous halfspaces to accuracy $\epsilon$ (prior
  work achieved $d^{(k/\epsilon)^{O(1)}}$).  We work under the mild assumption that the Gaussian
  training distribution contains at least an $\epsilon$ fraction of both positive and negative
  examples ($\epsilon$-balanced).  We also prove the first set of SQ lower-bounds for any
  TDS learning problem and show (1) the $\epsilon$-balanced assumption is necessary for $\mathsf{poly}(d,1/\epsilon)$-time
  TDS learning for a single halfspace and (2) a $d^{\tilde{\Omega}(\log (1/\epsilon))}$ lower bound
  for the intersection of two general halfspaces, even with the $\epsilon$-balanced assumption.
  Our techniques significantly expand the toolkit for TDS learning.  We use dimension
  reduction and coverings to give efficient algorithms for computing a localized version
  of discrepancy distance, a key metric from the domain adaptation literature.'
featured: true
publication: '**COLT 2024**'
url_pdf: https://proceedings.mlr.press/v247/klivans24b/klivans24b.pdf
links:
- name: URL
  url: https://proceedings.mlr.press/v247/klivans24b.html
---

