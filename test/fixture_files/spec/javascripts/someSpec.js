describe('Something', function() {
  it('does a thing', function() {
    expect(thingUnderTest.something).toBeTruthy();
  });
});

describe('weird encodings', function() {
  it('works', function() {
    expect(weirdEncoding).toEqual('ã');
  });
});
