import modal

# Define the app
app = modal.App("wise-oracle")

@app.function()
def run_wise():
    from wise import crew  # Import your crew
    crew.kickoff()  # Run the infinite loop

if __name__ == "__main__":
    with app.run():
        run_wise.remote()  # Start on cloud
