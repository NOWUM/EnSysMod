#!/bin/bash

declare -a BUMP_OPTIONS=("major" "minor" "patch")

### Increments the part of the string
## $1: version itself
## $2: number of part: 0 – major, 1 – minor, 2 – patch
increment_version() {
  local delimiter="."
  local array=($(echo "$1" | tr $delimiter '\n'))
  array[$2]=$((array[$2] + 1))
  if [ "$2" -lt 2 ]; then array[2]=0; fi
  if [ "$2" -lt 1 ]; then array[1]=0; fi
  echo "$(
    local IFS=$delimiter
    echo "${array[*]}"
  )"
}

### Require main branch
require_main_branch() {
  branch="$(git rev-parse --abbrev-ref HEAD)"
  if [[ "$branch" != "main" ]]; then
    echo "ERR: Please switch to main branch in order to run this script."
    exit 10
  else
    echo "OK: Currently on branch main."
  fi
}
### Require no uncommitted changes
require_no_uncommitted_changes() {
  if ! git diff-index --quiet HEAD --; then
    echo "ERR: Found uncommitted changes. Commit them in order to run this script."
    exit 11
  else
    echo "OK: No uncommitted changes found."
  fi
}

### Retrieve current version for project
get_current_version() {
  version=$(sed -n '/^__version__/,//p' ./ensysmod/__init__.py | sed -e 's/__version__ = "\(.*\)"/\1/')
  echo "$version"
}

### Update all files containing the version number
## $1: current version
## $2: new version
update_version() {
  sed -i "s/$1/$2/g" ./ensysmod/__init__.py
}

### Convert string into bump option index
## $1: bump option as string
get_bump_option() {
  index=-1
  for i in "${!BUMP_OPTIONS[@]}"; do
    if [[ "${BUMP_OPTIONS[$i]}" == "$1" ]]; then
      index=$i
      break
    fi
  done

  echo "$index"
}

### Main Script
cd "$(git rev-parse --show-toplevel)" || (
  echo "Couldn't find project folder. Please check your working dir."
  exit 1
)

BUMP=$(get_bump_option "$1")
if [[ "$BUMP" == -1 ]]; then
  echo "ERR: Please specify a correct bump option. Use$(printf " %s" "${BUMP_OPTIONS[@]}") as first parameter."
  exit 12
fi

echo "OK: Running release script for a ${BUMP_OPTIONS[BUMP]} bump ..."

require_main_branch
require_no_uncommitted_changes

# Handle version
CURRENT_VERSION=$(get_current_version)
echo "OK: Current version: $CURRENT_VERSION"

NEW_VERSION=$(increment_version "$CURRENT_VERSION" "$BUMP")
echo "OK: New version: $NEW_VERSION"

update_version "$CURRENT_VERSION" "$NEW_VERSION"

# Create and Push release branch
git pull origin main
git checkout -B "release/$NEW_VERSION"
git add .
git commit -m "Bump release version $CURRENT_VERSION -> $NEW_VERSION"
git push --set-upstream origin "release/$NEW_VERSION"

# Switch back to main branch
git checkout main
