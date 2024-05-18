class Helpers:
    """ Helpers """

    def get_item(self, data, keys):
        """ Access data with accessor """
        
        for key in keys:
            data = data[key]
        return data

    def parse_items(
        self,
        data,
        accessor,
        return_value,
        name_value,
        artists_value=False,
        artists_array=True,
    ):
        """ Parse tracks for questionary """

        choices     = []
        track_width = 0

        if artists_value:
            names = [
                self.get_item(item, name_value)
                for item in self.get_item(data, accessor)
            ]
            if names:
                track_width = max(map(len, names))

        for item in self.get_item(data, accessor):
            track_name = self.get_item(item, name_value)
            if artists_value:
                if artists_array:
                    artist_names = ", ".join(
                        artist["name"]
                        for artist in (self.get_item(item, artists_value))
                    )
                else:
                    artist_names = self.get_item(item, artists_value)
                choices.append(
                    {
                        "name": "{0:<{track_width}} -- {1}".format(
                            track_name, artist_names, track_width=track_width
                        ),
                        "value": self.get_item(item, return_value),
                    }
                )
            else:
                choices.append(
                    {
                        "name": track_name,
                        "value": self.get_item(item, return_value),
                    }
                )

        return choices

        