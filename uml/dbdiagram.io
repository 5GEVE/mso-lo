// Paste into https://dbdiagram.io/

Table NFVO_INFO {
  id int [pk]
  name varchar
  type varchar [not null]
  site varchar [not null]
  created_at datetime
  updated_at datetime
  uri varchar
}

Table NFVO_CREDENTIALS {
  id int [pk]
  nfvo_id varchar [ref: - NFVO_INFO.id]
  host varchar [not null]
  project varchar [not null]
  user varchar [not null]
  password varchar [not null]
}

Table NS_SUBSCRIPTION {
  id int [pk]
  nfvo_id varchar [ref: > NFVO_INFO.id]
  hostReport varchar [not null]
  ns_id varchar [not null]
}

