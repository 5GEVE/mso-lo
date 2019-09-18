# Paste into https://dbdiagram.io/

Table NFVO {
  id int [pk]
  name varchar
  type varchar [not null]
  site varchar [not null]
  created_at datetime
  updated_at datetime
  uri varchar
  host varchar [not null]
  user varchar [not null]
  password varchar [not null]
  project varchar [not null]
}

Table CatalogueSubscription as csub {
  id int [pk]
  hostReport varchar [not null]
  nfvo_id varchar [ref: > NFVO.id]
}

Table NSSubscription as nsub {
  id int [pk]
  hostReport varchar [not null]
  nfvo_id varchar [ref: > NFVO.id]
  ns_id varchar [not null]
}

