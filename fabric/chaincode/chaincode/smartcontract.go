// Author: Tianfu Gao
// Email: tfgao@stu.xidian.edu.cn
// License: GPL-3

package chaincode

import (
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing an Asset
type SmartContract struct {
	contractapi.Contract
}

type Asset struct {
	Domain         string  `json:"Domain"`
	Record         string  `json:"Record"`
	Owner          string  `json:"Owner"`
	CredibilityVal float64 `json:"CredibilityVal"`
	CredibilityUsr string  `json:"CredibilityUsr"`
}

// InitLedger adds a base set of assets to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	assets := []Asset{
		{Domain: "localhost", Record: "127.0.0.1", Owner: "Authority", CredibilityVal: 1, CredibilityUsr: "Authority"},
	}

	for _, asset := range assets {
		assetJSON, err := json.Marshal(asset)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(asset.Domain, assetJSON)
		if err != nil {
			return fmt.Errorf("failed to put to world state. %v", err)
		}
	}

	return nil
}

// CreateAsset issues a new asset to the world state with given details.
func (s *SmartContract) CreateAsset(ctx contractapi.TransactionContextInterface, domain string, record string, owner string, credibilityVal float64, credibilityUsr string) error {
	exists, err := s.AssetExists(ctx, domain)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the asset %s already exists", domain)
	}

	asset := Asset{
		Domain:		domain,
		Record:		record,
		Owner:		owner,
		CredibilityVal:	credibilityVal,
		CredibilityUsr:	credibilityUsr,
	}
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(domain, assetJSON)
}

// ReadAsset returns the asset stored in the world state with given id.
func (s *SmartContract) ReadAsset(ctx contractapi.TransactionContextInterface, domain string) (*Asset, error) {
	assetJSON, err := ctx.GetStub().GetState(domain)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if assetJSON == nil {
		return nil, fmt.Errorf("the asset %s does not exist", domain)
	}

	var asset Asset
	err = json.Unmarshal(assetJSON, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

// UpdateAsset updates an existing asset in the world state with provided parameters.
func (s *SmartContract) UpdateAsset(ctx contractapi.TransactionContextInterface, domain string, record string, owner string, credibilityVal float64, credibilityUsr string) error {
	exists, err := s.AssetExists(ctx, domain)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", domain)
	}

	// overwriting original asset with new asset
	asset := Asset{
		Domain:		domain,
		Record:		record,
		Owner:		owner,
		CredibilityVal:	credibilityVal,
		CredibilityUsr:	credibilityUsr,
	}
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(domain, assetJSON)
}

// DeleteAsset deletes an given asset from the world state.
func (s *SmartContract) DeleteAsset(ctx contractapi.TransactionContextInterface, domain string) error {
	exists, err := s.AssetExists(ctx, domain)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", domain)
	}

	return ctx.GetStub().DelState(domain)
}

// AssetExists returns true when asset with given ID exists in world state
func (s *SmartContract) AssetExists(ctx contractapi.TransactionContextInterface, domain string) (bool, error) {
	assetJSON, err := ctx.GetStub().GetState(domain)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return assetJSON != nil, nil
}

// TransferAsset updates the owner field of asset with given id in world state, and returns the old owner.
func (s *SmartContract) TransferAsset(ctx contractapi.TransactionContextInterface, domain string, newOwner string) (string, error) {
	asset, err := s.ReadAsset(ctx, domain)
	if err != nil {
		return "", err
	}

	oldOwner := asset.Owner
	asset.Owner = newOwner

	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return "", err
	}

	err = ctx.GetStub().PutState(domain, assetJSON)
	if err != nil {
		return "", err
	}

	return oldOwner, nil
}

// GetAllAssets returns all assets found in world state
func (s *SmartContract) GetAllAssets(ctx contractapi.TransactionContextInterface) ([]*Asset, error) {
	// range query with empty string for startKey and endKey does an
	// open-ended query of all assets in the chaincode namespace.
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var assets []*Asset
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var asset Asset
		err = json.Unmarshal(queryResponse.Value, &asset)
		if err != nil {
			return nil, err
		}
		assets = append(assets, &asset)
	}

	return assets, nil
}
