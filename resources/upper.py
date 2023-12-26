class Upper:
    def upper_data(self, data: dict) -> dict:
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.upper().strip()
        return data
