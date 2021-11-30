from resource import ResourceStack, RegisterType

RegisterType('roctorio:item:null:', {'tx_source': 'assets\\resources\\water-256.png',
                                     'limit': 0})

RegisterType('roctorio:item:water:', {'tx_source': 'assets\\resources\\water-256.png',
                                      'limit': 32,
                                      'tags': 'liquid'})

RegisterType('roctorio:item:ore:', {'tx_source': 'assets\\resources\\ore-256.png',
                                    'limit': 64,
                                    'tags': 'solid'})
