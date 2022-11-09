import api
import json
from solution import Solution
api_key = "b5403f80-8fdf-47b8-645f-08dabbf9e85f"   # TODO: Your api key here
# The different map names can be found on considition.com/rules
# TODO: You map choice here. Unless changed, the map "Suburbia" will be selected.
# map_name = "Suburbia"
map_name = "Sky Scrape City"
# TODO: You bag type choice here. Unless changed, the bag type 1 will be selected.
bag_type = 1
bagType_washtime = [1, 2, 3, 5, 7]
bagType_reusable = [0, 1, 3, 9, 12]


def main():
    print("Starting game...")
    days = 31 if map_name == "Suburbia" or map_name == "Fancyville" else 365
    newOrderList = [0] * days
    solution = Solution(True, 1.75, 0, 2)
    solution.orders = newOrderList
    # send a only 0 order list to get all negative data.
    submit_game_response = api.submit_game(api_key, map_name, solution)
    newOrderList = []
    dailys = submit_game_response.get('dailys')
    prevNeg = 0
    # base orders on the negative points since that seems to be when they want to make a purchase
    for day in dailys:
        negativeScore = day.get('negativeCustomerScore') - prevNeg
        prevNeg = day.get('negativeCustomerScore')
        orderAmount = int(abs(negativeScore)/10)
        newOrderList.append(orderAmount)
    solution.orders = newOrderList
    # send the new list with orders to get when people wants to return
    submit_game_response = api.submit_game(api_key, map_name, solution)
    dailys = submit_game_response.get('dailys')
    returnDays = [0] * days
    prevNeg = 0
    for index, day in enumerate(dailys):
        negativeScore = day.get('negativeCustomerScore') - prevNeg
        prevNeg = day.get('negativeCustomerScore')
        if (negativeScore < 0):
            returnDays[index] = int(abs(negativeScore)/10)

    for index, returnNumber in enumerate(returnDays):
        returnsLeft = returnNumber
        indexToSet = index + bagType_washtime[solution.bagType-1]
        if returnNumber > 0 and bagType_reusable[solution.bagType-1] != 0 and indexToSet + 1 < len(newOrderList):

            while returnsLeft > 0:
                if indexToSet + 1 < len(newOrderList):
                    break
                diff = newOrderList[indexToSet] - returnsLeft

                if (diff < 0):
                    newOrderList[indexToSet] = 0
                    returnsLeft = abs(diff)
                else:
                    newOrderList[indexToSet] = diff
                    returnsLeft = 0

                indexToSet += 1
    solution.refundAmount = 4
    submit_game_response = api.submit_game(api_key, map_name, solution)


if __name__ == "__main__":
    main()
