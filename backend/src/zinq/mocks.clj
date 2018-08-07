(ns zinq.mocks
  (:require
   [clojure.edn :as edn]
   [com.stuartsierra.component :as component]
   [zinq.interfaces :refer [Persistable]]
   [clojure.java.io :as io]))

;; adapters
(defrecord InMemoryStore [state]
  component/Lifecycle
  (start [component]
    component)
  (stop [component]
    (dissoc component :state))
  Persistable
  (lookup [_ thing id]
    (prn "looking up " id)
    (get-in state [thing id]))
  (save [_ thing data]
    (swap! state #(assoc-in % [thing (:id data)] data))))

(defn make-in-memory-store [init-state]
  (map->InMemoryStore {:state (atom init-state)}))

(defn make-demo-in-memory-store [filename]
  (with-open [reader (-> filename io/resource io/reader java.io.PushbackReader.)]
    (let [demo-state (edn/read reader)]
      (make-in-memory-store demo-state))))
