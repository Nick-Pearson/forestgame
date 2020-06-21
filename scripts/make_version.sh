#!/bin/bash
if [[ `git status --porcelain` ]]; then
  echo "ERROR: Repository has uncommitted changes"
  exit 1
fi

lastVersion=$(git describe)
readarray -d - -t strarr <<<"$lastVersion"
echo "Last version was: ${strarr[0]:1}"

# create a variable to hold the input
read -p "Next version: " version
 
if [[ -z "$version" ]]; then
   printf '%s\n' "ERROR: No input entered"
   exit 1
else
   printf "Preparing version %s \n" "$version"
   read -s -n 1 -p "Continue?"
fi

echo "\n"
git commit --allow-empty -m "Prepare version ${version}"
echo "Tagging commit v${version}"
git tag -a v${version} -m "Version ${version}"
git push --tags