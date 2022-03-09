CREATE TABLE pcap_table
             (  uuid VARCHAR(36) NOT NULL,
                utctimestamp DOUBLE 
                eth_src VARCHAR(25)
                eth_dst VARCHAR(25)
                eth_type VARCHAR(6)
                packet_length VARCHAR(100)
                ip_src VARCHAR(50)
                ip_dst VARCHAR(50)
                ip_version VARCHAR(10)
                ip_proto VARCHAR(10)
                ip_len VARCHAR(10)
                ip_ihl VARCHAR(10)
                ip_tos VARCHAR(10)
                ip_flags VARCHAR(10)
                ip_ttl VARCHAR(10)
                packet_load VARCHAR(100)
                load_count VARCHAR(10)
                protocol VARCHAR(10)
                protocol_sport VARCHAR(10)
                protocol_dport VARCHAR(10)
                score DOUBLE
                PRIMARY KEY (uuid)
             );