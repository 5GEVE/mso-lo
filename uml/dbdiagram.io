// Paste into https://dbdiagram.io/

Table NFVO {
  id int [pk]
  name varchar [not null]
  type varchar [not null]
  site varchar [not null]
  uri varchar
  created_at datetime
  updated_at datetime
}

Table NFVO_CREDENTIALS {
  nfvo_id int [ref: - NFVO.id, pk]
  host varchar [not null]
  project varchar [not null]
  user varchar [not null]
  password varchar [not null]
}

Table NS_SUBSCRIPTION {
  id int [pk]
  nfvo_id varchar [ref: > NFVO.id]
  callbackUri varchar [not null]
}

Table NS_INSTANCE {
  ns_id varchar [pk]
  sub_id varchar [ref: > NS_SUBSCRIPTION.id, pk]
}

