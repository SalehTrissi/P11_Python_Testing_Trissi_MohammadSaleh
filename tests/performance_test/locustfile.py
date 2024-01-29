from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def showSummary(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get("/book/Testing%20Date/Simply%20Lift")

    @task
    def purchasePlaces(self):
        # Replace these values with valid test data
        competition_name = "Testing Date"
        club_name = "Simply Lift"
        places_required = 12
        self.client.post("/purchasePlaces", {
            "competition": competition_name,
            "club": club_name,
            "places": places_required
        })

    @task
    def clubPointsList(self):
        self.client.get("/clubPointsList")
