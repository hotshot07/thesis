CREATE TABLE pcap_table(
   uuid VARCHAR(36) NOT NULL,
   utctimestamp DOUBLE PRECISION,
   packet_length VARCHAR(100),
   ip_src VARCHAR(50),
   source_internal VARCHAR(10),
   source_external VARCHAR(10),
   ip_dst VARCHAR(50),
   destination_internal VARCHAR(10),
   destination_external VARCHAR(10),
   protocol VARCHAR(10),
   protocol_sport VARCHAR(10),
   protocol_dport VARCHAR(10),
   score DOUBLE,
   PRIMARY KEY (uuid)
);