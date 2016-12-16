import route53

debug = False

class Route53Connection:
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_route53_zone):
        conn = route53.connect(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.zone = conn.get_hosted_zone_by_id(aws_route53_zone)

    def change_record(self, record_name, record_type, record_value):
        for record_set in self.zone.record_sets:
            if debug: print("record: {} {} {}".format(record_set.name, record_set.rrset_type, record_set.records[0]))
            if record_set.rrset_type == record_type and record_set.name == record_name:
                if debug: print("match: {} {} {}".format(record_set.name, record_set.rrset_type, record_set.records[0]))
                record_set.records = [record_value]
                record_set.save()
                return "OK"
        return "Record not found"

