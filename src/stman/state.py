class AppState:
    '''Since this project is relatively small, the 
    ui state and caching logic can be stored in the 
    same class and have no significant impact on debugging.
    This makes for cleaner code overall.'''

    def __init__(self):
        # State vars
        self.current_path = []
        self.selections = []
        self.should_exit = False
        self.show_cnc = True

        # Cache
        self.cache_library = {}
    
    # Cache functions
    def cache_set(self, key, value):
        if len(self.cache_library) >= 10:
            # Remove the oldest item
            oldest_key = next(iter(self.cache_library))
            del self.cache_library[oldest_key]
        
        self.cache_library[key] = value
    
    def cache_get(self, key):
        return self.cache_library.get(key)

    def cache_clear(self):
        self.cache_library.clear()