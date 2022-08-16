

1. Install Brownie

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
# restart your terminal
pipx install eth-brownie
```
Or, if that doesn't work, via pip
```bash
pip install eth-brownie
```

2. Testing
```bash
add a PRIVATE_KEY variable in your .env file, checkout the .env.sample for ref

run tests  by running 
brownie test  -s
```
