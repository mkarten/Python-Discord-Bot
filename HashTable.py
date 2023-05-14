class HashTable:
    def __init__(self):
        self.size = 1000  # initial size of the hash table
        self.table = [[] for _ in range(self.size)]  # create an empty table


    def _hash(self, key):
        # Generate a hash value for the given key
        return hash(key) % self.size

    def _get_bucket(self, key):
        # Get the bucket corresponding to the given key
        hash_value = self._hash(key)
        return self.table[hash_value]

    def __getitem__(self, key):
        # Get the value associated with the given key
        bucket = self._get_bucket(key)
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key, value):
        # Set the value associated with the given key
        bucket = self._get_bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def __delitem__(self, key):
        # Delete the key-value pair associated with the given key
        bucket = self._get_bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return
        raise KeyError(key)

    def __contains__(self, key):
        # Check if the given key is present in the hash table
        bucket = self._get_bucket(key)
        for k, v in bucket:
            if k == key:
                return True
        return False

    def __len__(self):
        # Get the number of key-value pairs in the hash table
        return sum(len(bucket) for bucket in self.table)

    def __str__(self):
        # Get a string representation of the hash table
        items = []
        for bucket in self.table:
            for k, v in bucket:
                items.append(f"{k}: {v}")
        return "{" + ", ".join(items) + "}"

    def __iter__(self):
        # Iterate over the key-value pairs in the hash table
        for bucket in self.table:
            for k, v in bucket:
                yield k, v
    def __getstate__(self):
        # Get the state of the object for pickling
        return dict(self)

    def __setstate__(self, state):
        # Restore the state of the object from pickled data
        self.size = 1000
        self.table = [[] for _ in range(self.size)]
        for k, v in state.items():
            self[k] = v