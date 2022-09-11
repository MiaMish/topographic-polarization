

Model:

In each iteration:



   For each individual i:

      Choose two traits t-choice,t-interaction

      Find a partner j for i:
         With probability p the partner j is chosen randomly
         Otherwise, it is chosen by proximity based on t-choice

      Interact based on t-interaction.

      If not successful:

         i moves its t-choice property away from that of j.
         If they are the same, movement in a random direction (1 or -1)

         constrain the property to the range [-1,1]



