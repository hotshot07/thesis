CREATE TABLE pcap_data4
             (
                           
                           eth_dst        VARCHAR(100),
                           eth_src       VARCHAR(100) ,
                           ip_dst         VARCHAR(100) ,
                           ip_flags       VARCHAR(10) ,
                           ip_ihl        VARCHAR(10) ,
                           ip_len         VARCHAR(10) ,
                           ip_proto       VARCHAR(10),
                           ip_src        VARCHAR(50),
                           ip_tos         VARCHAR(50) ,
                           ip_ttl         VARCHAR(10) ,
                           ip_version     VARCHAR(10) ,
                           packet_length          VARCHAR(10) ,
                           packet_data            VARCHAR(100),
                           load_count      VARCHAR(10) ,
                           protocol        VARCHAR(10) ,
                           protocol_dport  VARCHAR(10),
                           protocol_sport  VARCHAR(10) ,
                           score           INT
             );

