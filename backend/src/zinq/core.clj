(ns zinq.core
  (:require [ring.adapter.jetty :refer [run-jetty]]
            [compojure.core :refer :all]
            [compojure.route :as route]
            [com.stuartsierra.component :as component]
            [clojure.spec.alpha :as s]
            [zinq.interfaces :refer [Persistable]]
            [zinq.mocks :as mocks]
            [compojure.coercions :refer [as-uuid]]
            [zinq.adapters.menus :as menus]))

(defn make-handler [menu-repo]
  (routes
    (GET "/" [] "<h1>zinq</h1>")
    (GET "/api/menus/:id" [id :<< as-uuid]
         (prn-str (menus/get-menu menu-repo id)))
    (route/not-found "Not Found!")))

;; Application
(defrecord AppServer [config menu-repo]
  component/Lifecycle
  (start [{server :server :as component}]
    (if server
      component
      (update component
       :server
       (fn [& _] (run-jetty (make-handler menu-repo) {:port (:port config) :join? false})))))
  (stop [{server :server :as component}]
    (if server
      (try
        (.stop server)
        (prn "server stopped")
        (assoc component :server nil)
        (catch Exception e
          (prn (format "error stopping server %s" (.getMessage e)))
          component))
      component)))

(defn build-system [port]
  (component/system-map
   :config {:port port}
   :store (mocks/make-demo-in-memory-store "demo.edn" )
   :menu-repo (component/using (menus/map->MenuRepo {}) [:store])
   :server (component/using (map->AppServer {}) [:config :menu-repo])))

(def demo-system (build-system 3030))

(defn start-demo-system []
  (alter-var-root #'demo-system component/start))

(defn stop-demo-system []
  (alter-var-root #'demo-system component/stop))
