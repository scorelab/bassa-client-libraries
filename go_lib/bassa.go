//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License

package bassa

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"regexp"
	"time"

	"github.com/gojektech/heimdall"
	"github.com/gojektech/heimdall/httpclient"
	"github.com/hokaccha/go-prettyjson"

	logger "./utils/"
)


// Bassa : Bassa Go object
type Bassa struct {
	apiURL     string
	token      string
	timeout    int
	retryCount int
	httpClient *httpclient.Client
}

var (
	errBadFormat        = errors.New("invalid format")
	errIncompleteParams = errors.New("Some fields are not valid or empty")
	emailRegex	p.MustCompile("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")
)

// validateFormat : Helper function to validate email address
func validateFormat(email string) error {
	if !emailRegexp.MatchString(email) {
		return errBadFormat
	}
	return nil
}

// Init : Initialization of Bassa
func (b *Bassa) Init(apiURL string, timeout int, retryCount int) {
	if apiURL == "" || timeout == 0 {
		panic(errIncompleteParams)
	}
	u, err := url.Parse(apiURL)
	if err != nil {
		logger.InfoLogger.Println(u)
		logger.ErrorLogger.Panic(err)
	} else {
		b.apiURL = apiURL
		b.timeout = timeout
		b.retryCount = retryCount
		b.token = ""
		timeout := time.Duration(timeout) * time.Millisecond
		httpClient := httpclient.NewClient(
			httpclient.WithHTTPTimeout(timeout),
			httpclient.WithRetryCount(retryCount),
			httpclient.WithRetrier(heimdall.NewRetrier(heimdall.NewConstantBackoff(10*time.Millisecond, 50*time.Millisecond))),
		)
		b.httpClient = httpClient
	}
}

// Login : Function to login as a user
func (b *Bassa) Login(userName string, password string) {
	if userName == "" || password == "" {
		panic(errIncompleteParams)
	}
	endpoint := "/api/login"
	apiURL := b.apiURL + endpoint

	form := url.Values{}
	form.Add("user_name", userName)
	form.Add("password", password)

	response, err := http.PostForm(apiURL, form)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	defer response.Body.Close()
	b.token = response.Header["Token"][0]

	respBody, err := ioutil.ReadAll(response.Body)
	if err != nil {
		logger.InfoLogger.Println(string(respBody))
		logger.ErrorLogger.Panic(err)
	}
}

// AddRegularUserRequest : Function to login as a user
func (b *Bassa) AddRegularUserRequest(userName string, password string, email string) {
	if userName == "" || password == "" || email == "" {
		panic(errIncompleteParams)
	}

	err := validateFormat(email)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	endpoint := "/api/regularuser"
	apiURL := b.apiURL + endpoint

	requestBody, err := json.Marshal(map[string]string{
		"user_name": userName,
		"password":  password,
		"email":     email})
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(requestBody))
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()

	respBody, err := ioutil.ReadAll(response.Body)
	if err != nil {
		logger.InfoLogger.Println(string(respBody))
		logger.ErrorLogger.Panic(err)
	}
}

// AddUserRequest : Function to login as a user
func (b *Bassa) AddUserRequest(userName string, password string, email string, authLevel int) {
	if userName == "" || password == "" || email == "" {
		panic(errIncompleteParams)
	}

	err := validateFormat(email)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	endpoint := "/api/user"
	apiURL := b.apiURL + endpoint

	requestBody := []byte(fmt.Sprintf("{user_name:\"%s\", password: \"%s\", email: \"%s\", auth: %d}", userName, password, email, authLevel))

	request, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(requestBody))
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
}

// RemoveUserRequest : Function to remove user
func (b *Bassa) RemoveUserRequest(userName string) string {
	if userName == "" {
		panic(errIncompleteParams)
	}

	endpoint := "/api/user" + "/" + userName
	apiURL := b.apiURL + endpoint

	request, err := http.NewRequest("DELETE", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	return string(out)
}

// UpdateUserRequest : Function to update user request
func (b *Bassa) UpdateUserRequest(userName string, newUserName string, password string, authLevel int, email string) {
	if userName == "" || password == "" || email == "" || newUserName == "" {
		panic(errIncompleteParams)
	}

	err := validateFormat(email)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	endpoint := "/api/user"
	apiURL := b.apiURL + endpoint + "/" + userName

	requestBody := []byte(fmt.Sprintf("{user_name:\"%s\", password: \"%s\", email: \"%s\", auth_level: %d}", newUserName, password, email, authLevel))

	request, err := http.NewRequest("PUT", apiURL, bytes.NewBuffer(requestBody))
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
}

// GetUserRequest : Function to get user request
func (b *Bassa) GetUserRequest() string {

	endpoint := "/api/user"
	apiURL := b.apiURL + endpoint

	request, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
	return string(out)
}

// GetUserSignupRequests : Function to get user signup requests
func (b *Bassa) GetUserSignupRequests() string {

	endpoint := "/api/user/requests"
	apiURL := b.apiURL + endpoint

	request, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
	return string(out)
}

// ApproveUserRequest : Function to approve user request
func (b *Bassa) ApproveUserRequest(userName string) {
	if userName == "" {
		panic(errIncompleteParams)
	}
	endpoint := "/api/user/approve"
	apiURL := b.apiURL + endpoint + "/" + userName

	request, err := http.NewRequest("POST", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
}

// GetBlockedUserRequests : Function to get blocked user requests
func (b *Bassa) GetBlockedUserRequests() string {

	endpoint := "/api/user/blocked"
	apiURL := b.apiURL + endpoint

	request, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
	return string(out)
}

// BlockUserRequest : Function to block user request
func (b *Bassa) BlockUserRequest(userName string) {
	if userName == "" {
		panic(errIncompleteParams)
	}
	endpoint := "/api/user/blocked"
	apiURL := b.apiURL + endpoint + "/" + userName

	request, err := http.NewRequest("POST", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
}

// UnBlockUserRequest : Function to unblock user request
func (b *Bassa) UnBlockUserRequest(userName string) {
	if userName == "" {
		panic(errIncompleteParams)
	}
	endpoint := "/api/user/blocked"
	apiURL := b.apiURL + endpoint + "/" + userName

	request, err := http.NewRequest("DELETE", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
}

// GetDownloadUserRequests : Function to get download user requests
func (b *Bassa) GetDownloadUserRequests(limit int) string {
	if limit == 0 {
		limit = 1
	}
	endpoint := "/api/user/downloads"
	apiURL := b.apiURL + endpoint + "/" + string(limit)

	request, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
	return string(out)
}

// GetToptenHeaviestUsers : Function to get top ten heaviest users
func (b *Bassa) GetToptenHeaviestUsers() string {

	endpoint := "/api/user/heavy"
	apiURL := b.apiURL + endpoint

	request, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
	return string(out)
}

// StartDownload : Function to start download
func (b *Bassa) StartDownload(serverKey string) string {
	if serverKey == "" {
		serverKey = "123456789"
		logger.InfoLogger.Println("Server Key not given, continuing with: ", serverKey)
	}
	endpoint := "/api/download/start"
	apiURL := b.apiURL + endpoint

	request, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	request.Header.Set("key", serverKey)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
	return string(out)
}

// KillDownload : Function to kill download
func (b *Bassa) KillDownload(serverKey string) string {
	if serverKey == "" {
		serverKey = "123456789"
		logger.InfoLogger.Println("Server Key not given, continuing with: ", serverKey)
	}
	endpoint := "/api/download/kill"
	apiURL := b.apiURL + endpoint

	request, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	request.Header.Set("key", serverKey)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
	return string(out)
}

// AddDownloadRequest : Function to add download request
func (b *Bassa) AddDownloadRequest(downloadLink string) {
	if downloadLink == "" {
		panic(errIncompleteParams)
	}

	endpoint := "/api/download"
	apiURL := b.apiURL + endpoint

	requestBody, err := json.Marshal(map[string]string{
		"link": downloadLink})
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(requestBody))
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()

	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
}

// RemoveDownloadRequest : Function to remove download request
func (b *Bassa) RemoveDownloadRequest(id int) {

	endpoint := "/api/download"
	apiURL := b.apiURL + endpoint + string(id)

	request, err := http.NewRequest("DELETE", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()

	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
}

// RateDownloadRequest : Function to rate a download request
func (b *Bassa) RateDownloadRequest(id int, rate int) {
	if rate == 0 {
		logger.InfoLogger.Println("Continuing with 0 rating")
	}
	endpoint := "/api/download"
	apiURL := b.apiURL + endpoint + string(id)
	requestBody, err := json.Marshal(map[string]int{
		"rate": rate})
	request, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(requestBody))
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()

	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
}

// GetDownloadRequests : Function to get all download requests
func (b *Bassa) GetDownloadRequests(limit int) string {
	if limit == 0 {
		panic(errIncompleteParams)
	}
	endpoint := "/api/downloads"
	apiURL := b.apiURL + endpoint + "/" + string(limit)

	request, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
	return string(out)
}

// GetDownloadRequest : Function to get a download request
func (b *Bassa) GetDownloadRequest(id int) string {

	endpoint := "/api/download"
	apiURL := b.apiURL + endpoint + "/" + string(id)

	request, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
	return string(out)
}

// StartCompression : Function to start compression of files
func (b *Bassa) StartCompression(gidList []string) {
	if len(gidList) == 0 {
		panic(errIncompleteParams)
	}
	endpoint := "/api/compress"
	apiURL := b.apiURL + endpoint
	requestBody, err := json.Marshal(map[string][]string{
		"gid": gidList})
	request, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(requestBody))
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
}

// GetCompressionProgress : Function to get compression progress
func (b *Bassa) GetCompressionProgress(id int) string {

	endpoint := "/api/compression-progress"
	apiURL := b.apiURL + endpoint + "/" + string(id)

	request, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
	return string(out)
}

// SendFileFromPath : Function to send file from the local server
func (b *Bassa) SendFileFromPath(id int) string {

	endpoint := "/api/file"
	apiURL := b.apiURL + endpoint
	requestBody, err := json.Marshal(map[string]int{
		"gid": id})
	request, err := http.NewRequest("GET", apiURL, bytes.NewBuffer(requestBody))
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}
	request.Header.Set("token", b.token)
	response, err := b.httpClient.Do(request)
	if err != nil {
		logger.ErrorLogger.Panic(err)
	}

	defer response.Body.Close()
	var r interface{}
	if err := json.NewDecoder(response.Body).Decode(&r); err != nil {
		logger.ErrorLogger.Panic(err)
	}
	out, err := prettyjson.Marshal(r)
	logger.InfoLogger.Println(string(out))
	return string(out)
}
