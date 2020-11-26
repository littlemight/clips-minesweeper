(deftemplate bomb-pos
    (slot x (type NUMBER))
    (slot y (type NUMBER))
)
(deftemplate empty-slot
    (slot x (type NUMBER))
    (slot y (type NUMBER))
)
(deftemplate safe-pos
    (slot x (type NUMBER))
    (slot y (type NUMBER))
    (slot val (type NUMBER))
)
(deftemplate is-safe-around
    (slot x (type NUMBER))
    (slot y (type NUMBER))
)
(deftemplate is-unsafe-around
    (slot x (type NUMBER))
    (slot y (type NUMBER))
)
(deftemplate bomb-at
    (slot x (type NUMBER))
    (slot y (type NUMBER))
)
(deftemplate safe-at
    (slot x (type NUMBER))
    (slot y (type NUMBER))
)
(defrule mark-bomb
    (index-x $? ?ax ?x ?bx $?)
    (index-y $? ?ay ?y ?by $?)
    (empty-slot (x ?x) (y ?y))
    (or 
        (or
            (or
                (is-unsafe-around (x ?ax) (y ?ay))
                (is-unsafe-around (x ?ax) (y ?y))
            )
            (or
                (is-unsafe-around (x ?ax) (y ?by))
                (is-unsafe-around (x ?x) (y ?ay))
            )
        )
        (or
            (or
                (is-unsafe-around (x ?x) (y ?by))
                (is-unsafe-around (x ?bx) (y ?ay))
            )
            (or
                (is-unsafe-around (x ?bx) (y ?y))
                (is-unsafe-around (x ?bx) (y ?by))
            )
        )
    )
=>
    (assert (bomb-at (x ?x) (y ?y)))
)
(defrule mark-safe
    (index-x $? ?ax ?x ?bx $?)
    (index-y $? ?ay ?y ?by $?)
    (empty-slot (x ?x) (y ?y))
    (or 
        (or
            (or
                (is-safe-around (x ?ax) (y ?ay))
                (is-safe-around (x ?ax) (y ?y))
            )
            (or
                (is-safe-around (x ?ax) (y ?by))
                (is-safe-around (x ?x) (y ?ay))
            )
        )
        (or
            (or
                (is-safe-around (x ?x) (y ?by))
                (is-safe-around (x ?bx) (y ?ay))
            )
            (or
                (is-safe-around (x ?bx) (y ?y))
                (is-safe-around (x ?bx) (y ?by))
            )
        )
    )
=>
    (assert (safe-at (x ?x) (y ?y)))
)
