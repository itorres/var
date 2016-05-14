(define-module (foo bar)
  #:export (frob j0))

(define (frob x) (* 2 x))
(load-extension "./libguile-bessel" "init_bessel")
