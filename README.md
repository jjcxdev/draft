# Fantasy Draft Assistant

## Introduction

The Fantasy Draft Assistant is a Python-based tool designed to assist users in picking the best possible team for a fantasy football league. With a specified starting formation (e.g., G1 D3 M4 F3) and a set of reserve positions (e.g., D2 M2 F2), the program intelligently recommends players based on available data and dynamically updates options as positions are filled.

## Features

- **Automated Player Recommendations**: Offers real-time suggestions for your starting XI and reserves.
- **Team Formation Compliance**: Selects players according to a predefined formation and reserve criteria.
- **Dynamic Updates**: Updates recommendations based on selections and players picked by other managers.
- **Final Team Display**: Displays your final starting XI and reserves once the draft is complete.

## Requirements

- Python 3.x
- Pandas Library

## Usage

1. **Preparation**: A CSV file named `data.csv` containing player data (including names, positions, and fantasy points) should be present in the repository.

2. **Configuration**: Set up your starting formation and reserve criteria as required.

3. **Execution**: Run the `draft.py` script and follow the prompts to select players and build your team.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/jjcxdev/draft.git
   ```

2. Navigate to the project directory:

   ```bash
   cd draft
   ```

3. Install the required dependencies:

   ```bash
   pip install pandas
   ```

4. Run the main script:

   ```bash
   python draft.py
   ```
   
## Contribution

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/jjcxdev/draft/issues) or open a [pull request](https://github.com/jjcxdev/draft/pulls).

## License

[MIT License](LICENSE)

## Contact

Justin Chambers - j@jjcx.dev
