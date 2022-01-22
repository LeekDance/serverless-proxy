/**
  * @param params Call parameter, request body under HTTP request
  * @param context Call context
  *
  * @return The return data of the function will be used as Response Body in the HTTP scenario.
  *
  * For full information, please refer to:
  * https://inspirecloud-us.bytedance.net/docs/cloud-function/basic.html
  */

module.exports = async function(params, context) {
  let url = context.query['x-src'] || context.headers['x-src'] || 'https://httpbin.org/anything';
  delete context.query['x-src'];
  delete context.headers['x-src'];
  ignore_headers = ['x-tt-session-v2', 'host', 'x-bytefaas-event-type', 'x-bytefaas-function-id', 'x-bytefaas-request-id', 'x-bytefaas-revision-id', 'x-cdn-flag', 'x-client-scheme', 'x-cluster', 'x-forwarded-for', 'x-forwarded-host', 'x-forwarded-proto', 'x-forwarded-protocol', 'x-idc', 'x-psm', 'x-real-ip', 'x-real-port', 'x-server-name', 'x-ss-birth', 'x-ss-rid', 'x-tlb-cluster', 'x-tlb-server-name', 'x-toutiao-lb-ip', 'x-tt-logid'];
  for (header in ignore_headers) {
    delete context.headers[ignore_headers[header]];
  }
  if (!context.body || context.body === 'null') {
    delete context.headers['content-type'];
  }
  let request = {
    url: url,
    method: context.method,
    headers: context.headers,
    params: context.query,
  };
  if (context.body && context.body !== 'null') {
    request.data = context.body;
  }
  console.log(request);
  request['responseType'] = 'arraybuffer';
  const response = await axios.request(request);
  context.status(response.status);
  for (const header in response.headers) {
    context.set(header, response.headers[header]);
  }
  return response.data;
}
