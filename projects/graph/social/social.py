import random

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return (len(self.queue))

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        if avgFriendships > numUsers:
            print("Number of users must be greater than average number of friendships.")
            return
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}
        for i in range(1, numUsers + 1):
            self.addUser(f'user_{i}')
        ids = list(self.users.keys())
        i = 0
        while i < numUsers*avgFriendships/2:
            friendship_created = False
            while not friendship_created:
                filtered_ids = ids
                user_one = random.choice(filtered_ids)
                filtered_ids = [id for id in ids if id != user_one]
                user_two = random.choice(filtered_ids)
                if user_one not in self.friendships[user_two] and user_two not in self.friendships[user_one]:
                    self.addFriendship(user_one, user_two)
                    friendship_created = True
            i += 1
        set_len = 0
        for k, v in self.friendships.items():
            set_len += len(v)
        print(set_len)


    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        extended_network = {}
        user_ids = list(self.users.keys())

        def bfs(start, destination):
            visited = {}
            q = Queue()
            q.enqueue([start])
            while q.size() > 0:
                path = q.dequeue()
                v = path[-1]
                if v not in visited:
                    if destination == v: return path
                    visited[v] = True
                    for friend in self.friendships[v]:
                        new_path = list(path)
                        new_path.append(friend)
                        q.enqueue(new_path)



        for user_id in user_ids:
            extended_network[user_id] = bfs(userID, user_id)



        return extended_network


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populateGraph(20, 2)
    print(sg.friendships)
    connections = sg.getAllSocialPaths(1)
    print(connections)
