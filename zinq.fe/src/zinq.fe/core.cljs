(ns ^:figwheel-hooks zinq.fe.core
  (:require
   [goog.dom :as gdom]
   [clojure.string :as s]
   [reagent.core :as r :refer [atom]]
   [reagent.dom :as rdom]))

(println "This text is printed from src/hello_world/core.cljs. Go ahead and edit it and see reloading in action.")

(defn format-price [price]
  (let [[msp lsp] (s/split (/ price 100) #"\.")]
    (str "€ " msp "," lsp)))

(def demo-products
  [{:cat "warm" :key 124 :id 124 :name "Thee" :description "Warm" :price 235}
   {:cat "bier" :key 123 :id 123 :name "Duvel" :description "duivels lekker" :price 666}])

(defonce app-state (r/atom {:selected {}
                            :products demo-products
                            :step :menu}))

(defn dec-but-not-below-0
  [n]
  (max 0 (dec n)))

(defn product-component
  "Component that displays 1 product."
  [{:keys [id name description price]}]
  [:div.product {
    :data-id id
    :on-click #(swap! app-state update :expanded-product (constantly id))}
   [:div.product-top
    [:h3 name
     [:span.grey description]]
    [:div.price (format-price price)]]
   (when (= id (get @app-state :expanded-product))
     [:div.product-bottom
      [:div.amount-wrapper
       [:span.amount (get-in @app-state [:selected id] 0)]
       [:a.plus
        {:href "#"
         :on-click
         #(swap! app-state update-in [:selected id] inc)}
        "+"]
       [:a.min
        {:href "#"
         :on-click
         #(swap! app-state update-in [:selected id] dec-but-not-below-0)}
        "-"]]])])

(defn product-category [_ _]
  (let [visibility (r/atom true)]
    (fn [category products]
      [:div {:key category}
       [:h2
        {:on-click #(swap! visibility not)}
        category
        [:span.arrow-down]]
       (when @visibility
         [:div#products
          (for [product products]
             ^{:key (:id product)} [product-component product])])])))

(defn total-selected []
  (apply + (vals (:selected @app-state))))

(defn basket-component
  "Contains information about the selected items for order"
  []
  [:div#basket
   [:span#items-counter (total-selected) " items"]
   (when (> (total-selected) 0)
     [:a#order {:on-click #(swap! app-state update :step (constantly :waiting))
                :href "#"} "Bestellen"
      [:span.arrow-right]])])

(defn product-overview-component []
  [:div#product-overview
   [:div#items
   (for [[k v] (group-by :cat (:products @app-state))]
       ^{:key k} [product-category k v])
    [basket-component]]])

(defn waiting-component []
  [:form {:action "/pay" :method "POST"}
    [:script {
      :async true
      :src "https://checkout.stripe.com/checkout.js"
      :class "stripe-button"
      :data-key "pk_test_zMA8enjpMXxak5u07IHd38A4"
      :data-amount "999"
      :data-name "zinq"
      :data-description "Example charge"
      :data-image "https://stripe.com/img/documentation/checkout/marketplace.png"
      :data-locale "auto"
      :data-zip-code "true"
      :data-currency "eur"}]])

(defn done-component []
  [:div "Done"])

(defn menu-component []
  (fn []
    (case (get @app-state :step)
      :menu [product-overview-component]
      :waiting [waiting-component]
      :done [done-component])))


;; define your app data so that it doesn't get over-written on reload

(defn get-app-element []
  (gdom/getElement "app"))

(defn mount [el]
  (rdom/render [menu-component] el))


(defn mount-app-element []
  (when-let [el (get-app-element)]
    (mount el)))

;; conditionally start your application based on the presence of an "app" element
;; this is particularly helpful for testing this ns without launching the app
(mount-app-element)

;; specify reload hook with ^;after-load metadata
(defn ^:after-load on-reload []
  (mount-app-element)
  ;; optionally touch your app-state to force rerendering depending on
  ;; your application
  (swap! app-state update-in [:__figwheel_counter] inc))
