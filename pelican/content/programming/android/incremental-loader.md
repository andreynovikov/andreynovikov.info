Title: Implementing Android incremental loader
Date: 2016-03-31 17:37
Modified: 2016-04-01 14:42
Category: Программирование
Tags: android
Slug: programming-android-incremental-loader
Lang: en
Translation: no

There is an outstanding article on [implementing Android loaders](http://www.androiddesignpatterns.com/2012/08/implementing-loaders.html). However it covers classic pattern when data is being reloaded each time any part of it is modified. In my case I had to manipulate huge files, some of them taking minutes to load, so I could not afford reloading them on each data set change.

<!-- PELICAN_END_SUMMARY -->

That's why I have extended logic of my Loader to support incremental loading.

First, we define structure that will hold data state:

    :::java
    private final Set<String> mFiles = new HashSet<>();

We hold loaded data as usual:

	:::java
    private List<DataSource> mData;

When Loader starts it delivers already available data and initiates data change observer. If any data is added or removed data state holder is updated.

    :::java
    @Override
    protected void onStartLoading() {
        if (mData != null) {
            // Deliver any previously loaded data immediately, note that
            // deliverResult() gets newly added data instead of full data
            // in our case
            deliverResult(new ArrayList<DataSource>());
        }

        // Begin monitoring the underlying data source
        if (mObserver == null) {
            final File dir = getContext().getExternalFilesDir("data");
            if (dir == null)
                return;

            mObserver = new FileObserver(dir.getAbsolutePath(),
            				FileObserver.CLOSE_WRITE |
                            FileObserver.MOVED_FROM |
                            FileObserver.MOVED_TO |
                            FileObserver.DELETE) {
                @Override
                public void onEvent(int event, String path) {
                    if (event == 0x8000) // Undocumented, sent on stop watching
                        return;
                    if (path == null) // Undocumented, unexplainable
                        return;
                    path = dir.getAbsolutePath() + File.separator + path;
                    synchronized (mFiles) {
                        boolean loadedSource = false;
                        for (Iterator<DataSource> i = mData.iterator(); i.hasNext(); ) {
                            DataSource source = i.next();
                            if (source.path.equals(path)) {
                                if (source.isLoaded())
                                    loadedSource = true;
                                else
                                    i.remove();
                            }
                        }
                        if (!loadedSource) {
                            // Indicate state change by simply removing file
                            // reference from state holder
                            mFiles.remove(path);
                            DataLoader.this.onContentChanged();
                        }
                    }
                }
            };
            mObserver.startWatching();
        }

        if (takeContentChanged() || mData == null) {
            forceLoad();
        }
    }

Background loading starts, but in our case it should return only updated delta, not the full data set. We check data state and skip previously loaded data.

    :::java
    @Override
    public List<DataSource> loadInBackground() {
        Context ctx = getContext();
        File dataDir = ctx.getExternalFilesDir("data");
        if (dataDir == null)
            return null;
        File[] files = dataDir.listFiles();
        if (files == null)
            return null;

        List<DataSource> data = new ArrayList<>();

        for (File file : files) {
            if (isLoadInBackgroundCanceled())
                return null;
            synchronized (mFiles) {
                // Skip already loaded data
                if (mFiles.contains(path))
                    continue;
            }
            try {
                FileInputStream inputStream = new FileInputStream(file));
                DataSource source = loadData(inputStream;
                source.path = file.getAbsolutePath();
                source.setLoaded();
                data.add(source);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return data;
    }

When result is ready we join existing data with newly loaded data.

    :::java
    @Override
    public void deliverResult(List<DataSource> data) {
        if (isReset()) {
            return;
        }

        synchronized (mFiles) {
            if (mData == null) {
                mData = data;
            } else {
                // Somewhere under the hood it looks if the data has changed
                // by comparing object instances, so we need a new object
                ArrayList<DataSource> newData = new ArrayList<>(mData.size());
                newData.addAll(mData);
                newData.addAll(data);
                mData = newData;
            }

            for (DataSource source : data) {
                mFiles.add(source.path);
            }
        }

        if (isStarted())
            super.deliverResult(mData);
    }

Data is delivered to consumer in a full set but all object instances are preserved thus not breaking the data manipulation logic of data consumer.

Here arrives a good question: what happens when data consumer updates or deletes some data? This means that corresponding file will be modified or removed and observer will detect that. This case is already handled by the code. May be you have noticed a call to `source.isLoaded()` - this is the flag of internal data state. When data is loaded and consumer then modifies it, flag is set and Loader just skips the corresponding file. If data is wished to be removed, corresponding file is deleted and that flag is unset. In that case Loader removes data associated with this file.
