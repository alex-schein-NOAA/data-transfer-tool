from rrfs import Rrfs

import boto3

#%%

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)
    
#%%

# might just be better to take the ideas from RRFS code (i.e. AWS interfacing, maybe object-oriented) and write own code

# Step 1: establish master list of filenames (possible to scrape from AWS?)
    # Careful of date ranges if doing 2+ datasets, e.g. URMA and HRRR, need to take only shared dates, but this might just be fine to do manually
# Step 2: from this master date list, generate appropriate list of filenames
    # This is unnecessary if can just fetch list of names from AWS and subset those to only what's needed
# Step 3: loop over filename list, do the following
    # Fetch from appropriate AWS source
        # Might include switch statement or different functions (if in a class) for HRRR/URMA/else
    # ONLY IF THIS SAVES SIGNIFICANT STORAGE SPACE
    # IF IT DOESN'T, ONLY HAVE A FETCHER FUNC AND THEN LOOP OVER ALL DOWNLOADED FILES AFTERWARDS
        # Subset down to 2m temp and relevant spatial vars
        # Spatially restrict this to whatever domain (have as input arg)
        # Delete original file to save space (no point in caching, for what I'm doing)
        