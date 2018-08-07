(ns frontend.core
  (:require [reagent.core :as r]
            [clojure.string :as s]))

(enable-console-print!)

(defn format-price [price]
  (let [[msp lsp] (s/split (/ price 100) #"\.")]
    (str "€ " msp "," lsp)))

(def demo-products
  [{:cat "warm" :key 124 :id 124 :name "Thee" :description "Warm" :price 235}
   {:cat "bier" :key 123 :id 123 :name "duvel" :description "duivels lekker" :price 666}])

(defonce app-state (r/atom {:selected {}
                            :step :menu}))

(defn dec-but-not-below-0
  [n]
  (max 0 (dec n)))

(defn product-component
  "Component that displays 1 product."
  [{:keys [id name description price] :as all}]
  [:div.product {:data-id id
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

(defn product-category [category products]
  (let [visibility (r/atom true)
        selected (r/atom 0)]
    (fn [category products]
      [:div {:key category}
       [:h2
        {:on-click #(swap! visibility not)}
        category
        [:span.arrow-down]]
       (when @visibility
         [:div#products
          (doall
           (for [product products]
             [product-component product]))])])))

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
    [product-category "bier" demo-products]
    [basket-component]]]) 

(defn done-component []
  [:div "Done"])

(defn menu-component []
  (fn []
    (case (get @app-state :step)
      :menu [product-overview-component]
      :waiting [waiting-component]
      :done [done-component])))

(r/render
   [menu-component]
   (.getElementById js/document "app"))
