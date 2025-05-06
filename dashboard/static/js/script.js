<script>
    // Example to call refresh token every 4 mins
    setInterval(() => {
        fetch('/token/refresh/', {
            method: 'POST',
            credentials: 'include'  // Required to send cookies
        })
            .then(response => response.json())
            .then(data => {
                console.log('Access token refreshed');
            });
    }, 4 * 60 * 1000); // every 4 minutes
</script>