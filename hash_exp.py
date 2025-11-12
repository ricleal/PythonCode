def dict_hash(d):
    return hash(frozenset(d.items()))


# organizations.Account
d = {
    "Arn": "arn:aws:organizations::897722685872:account/o-xkabkmxmax/897722685872",
    "Email": "jkline@trustle.com",
    "Id": "897722685872",
    "JoinedMethod": "INVITED",
    "JoinedTimestamp": "2025-01-30T09:36:41.684000-08:00",
    "Name": "jkline-trustle",
    "Status": "ACTIVE",
}
h = dict_hash(d)

print(h)
