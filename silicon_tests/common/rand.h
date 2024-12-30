unsigned int  rand_num_gen(unsigned int * seed) {
    // Static LFSR state to maintain across function calls
    unsigned int  lfsr = * seed;  // Initial non-zero seed
    static int initialized = 0;        // To initialize LFSR on the first call
    unsigned int  feedback;

    // Initialize LFSR only once
    if (!initialized) {
        initialized = 1;
    }

    // Save the current LFSR value to return
    unsigned int  random_value = lfsr;

    // Compute feedback using a maximal-length polynomial x^32 + x^22 + x^2 + x^1 + 1
    feedback = ((lfsr >> 0) ^ (lfsr >> 1) ^ (lfsr >> 21) ^ (lfsr >> 31)) & 1;

    // Shift LFSR and insert feedback bit
    lfsr = (lfsr >> 1) | (feedback << 31);

    *seed = lfsr;
    return random_value;
}