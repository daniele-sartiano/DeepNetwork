from ..reader import FlowReader
import orjson

class CentoReader(FlowReader):

    # FIRST_SWITCHED|LAST_SWITCHED|VLAN_ID|IN_SRC_MAC|IN_DST_MAC|IP_PROTOCOL_VERSION|PROTOCOL|IP_SRC_ADDR|L4_SRC_PORT|IP_DST_ADDR|L4_DST_PORT|DIRECTION|INPUT_SNMP|OUTPUT_SNMP|SRC_PKTS|SRC_BYTES|DST_PKTS|DST_BYTES|TCP_FLAGS|SRC_TOS|DST_TOS|CLIENT_NW_LATENCY_MS|SERVER_NW_LATENCY_MS|L7_PROTO|L7_PROTO_NAME|DNS_QUERY|DNS_QUERY_TYPE|DNS_RET_CODE|HTTP_HOST|HTTP_URL|HTTP_RET_CODE
    
    def __init__(self, input):
        super().__init__(input)
        self.header = None

    @staticmethod
    def _hosts(data):
        return '{}_{}'.format(data['IN_SRC_MAC'], data['IPV4_SRC_ADDR']), '{}_{}'.format(data['IN_DST_MAC'], data['IPV4_DST_ADDR'])

    def read(self):
        for row in self.input:
            if row.startswith('#'):
                continue
            data = orjson.loads(row)
            if self.header is None:
                self.header = data.keys()
            self.n_flows += 1
            for h in self._hosts(data):
                self.hosts.add(h)
            yield data
