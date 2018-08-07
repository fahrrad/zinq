(ns zinq.adapters.menus
  (:require [com.stuartsierra.component :as component]
            [zinq.interfaces :as interfaces]))

(defrecord MenuRepo [store]
  component/Lifecycle
  (start [component]
    component)
  (stop [component]
    component))

(defn get-menu [menu-repo id]
  (prn "in repo, getting menu from store " (:store menu-repo))
  (interfaces/lookup (:store menu-repo) :menus id))
