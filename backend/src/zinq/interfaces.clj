(ns zinq.interfaces)

;; Interfaces
(defprotocol Persistable
  (lookup [store thing id])
  (save [store thing data]))
