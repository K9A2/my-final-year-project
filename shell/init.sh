#   Make dictionary structure for storing results
!<<comment
reuslt {
    true_topo {
        dc1_to_lan {
            benchmark {
                // 24 hours    
            };
            test_0 {
                // 12 hours
            };
            test_1 {
                // 12 hours
            };
            test_2 {
                // 12 hours
            };
            test_3 {
                // 12 hours
            }
        };
        dc2_to_amazon {
            benchmark {
                // 24 hours    
            };
            test_0 {
                // 12 hours
            };
            test_1 {
                // 12 hours
            };
            test_2 {
                // 12 hours
            };
            test_3 {
                // 12 hours
            }
        };
        dc1_to_sjtu {
            benchmark {
                // 24 hours    
            };
            test_0 {
                // 12 hours
            };
            test_1 {
                // 12 hours
            };
            test_2 {
                // 12 hours
            };
            test_3 {
                // 12 hours
            }
        };
        dc2_to_dc2 {
            benchmark {
                // 24 hours    
            };
            test_0 {
                // 12 hours
            };
            test_1 {
                // 12 hours
            };
            test_2 {
                // 12 hours
            };
            test_3 {
                // 12 hours
            }
        };
        lan_to_lan {
            benchmark {
                // 24 hours    
            };
            test_0 {
                // 12 hours
            };
            test_1 {
                // 12 hours
            };
            test_2 {
                // 12 hours
            };
            test_3 {
                // 12 hours
            }
        }
    };
    mininet {

    }
}
comment
mkdir result
cd result

    mkdir true_topo
    cd true_topo
        mkdir dc1_to_lan
        cd dc1_to_lan
            mkdir benchmark
            mkdir test_0
            mkdir test_1
            mkdir test_2
            mkdir test_3
        cd ../

        mkdir dc2_to_amazon
        cd dc2_to_amazon
            mkdir benchmark
            mkdir test_0
            mkdir test_1
            mkdir test_2
            mkdir test_3
        cd ../

        mkdir dc1_to_sjtu
        cd dc1_to_sjtu
            mkdir benchmark
            mkdir test_0
            mkdir test_1
            mkdir test_2
            mkdir test_3
        cd ../

        mkdir dc2_to_dc2
        cd dc2_to_dc2
            mkdir benchmark
            mkdir test_0
            mkdir test_1
            mkdir test_2
            mkdir test_3
        cd ../

        mkdir lan_to_lan
        cd lan_to_lan
            mkdir benchmark
            mkdir test_0
            mkdir test_1
            mkdir test_2
            mkdir test_3
        cd ../
    
    cd ../

    mkdir mininet

cd ../

chmod -R 777 result
