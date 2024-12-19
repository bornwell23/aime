@echo "Invalidating server node cache"
cd server
rm -rf node_modules
rm package-lock.json
cd ..

@echo "Invalidating ui node cache"
cd ui
rm -rf node_modules
rm package-lock.json

@echo "Invalidating vue cache"
vue-cli-service clean
cd ..

@echo "Re-installing dependencies"
start cmd /c "cd server && npm install"
start /wait cmd /c "cd ui && npm install"