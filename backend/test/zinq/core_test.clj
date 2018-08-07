(ns zinq.core-test
  (:require [clojure.test :refer :all]
            [zinq.core :refer :all]
            [com.stuartsierra.component :as component]
            [ring.mock.request :as mock]
            [zinq.adapters.menus :as menus]
            [zinq.mocks :as mocks]
            [clojure.pprint :as pprint]
            [clj-http.client :as http])
  (:import [java.util UUID]))



(def test-system
  (component/system-map
   :config {:port 3210}
   :store (mocks/make-demo-in-memory-store "demo.edn" )
   :menu-repo (component/using (menus/map->MenuRepo {}) [:store])
   :server (component/using (map->AppServer {}) [:config :menu-repo])))

(defn start-test-system [t]
  (component/start test-system)
  (t)
  (component/stop test-system))

(use-fixtures :once start-test-system)

(deftest handler-root-test
  (testing "getting a root returns 200"
    (is (= 200 (:status (http/get "http://localhost:3210/"))))))

(deftest handler-not-found-test
  (testing "unknown resource returns 404"
    (is (= 404 (:status (http/get "http://localhost:3210/woekie"  {:throw-exceptions false}))))))

(deftest handler-menu-with-id
  (testing "getting a menu by id returns a 200"
    (is (= 200 (:status (http/get "http://localhost:3210/api/menus/8f26d4ab-beb8-43dd-856b-eda67e992572")))))
  (testing "a menu consists of an id and a list of menu items"
    (let [id "8f26d4ab-beb8-43dd-856b-eda67e992572"
          uuid (UUID/fromString id)
          response (http/get (str "http://localhost:3210/api/menus/" id) )
          _ (prn "response: " response)
          {id-from-response :id menu-items :menu-items} (:body response)]
      (is (= id id-from-response)))))
