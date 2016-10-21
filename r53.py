import route53

AWS_ACCESS_KEY_ID     = "AKIAIQKRT7R5AAO6K6YQ"
AWS_SECRET_ACCESS_KEY = "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"
AWS_ROUTE53_ZONE      = "Z1HMB761DV99GU"

record       = "tekumo.fi."
record_type  = "A"
record_value = "123.123.123.123"

class Route53Connection:
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_route53_zone):
        conn = route53.connect(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        self.zone = conn.get_hosted_zone_by_id(AWS_ROUTE53_ZONE)

    def change_record(self, record_name, record_type, record_value):
        for record_set in self.zone.record_sets:
            if record_set.rrset_type == record_type and record_set.name == record:
                #print("match: {} {} {}".format(record_set.name, record_set.rrset_type, record_set.records[0]))
                record_set.records = [record_value]
                record_set.save()

