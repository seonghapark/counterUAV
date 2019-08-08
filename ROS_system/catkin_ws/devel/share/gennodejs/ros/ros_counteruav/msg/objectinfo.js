// Auto-generated. Do not edit!

// (in-package ros_counteruav.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class objectinfo {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.who = null;
      this.time = null;
    }
    else {
      if (initObj.hasOwnProperty('who')) {
        this.who = initObj.who
      }
      else {
        this.who = '';
      }
      if (initObj.hasOwnProperty('time')) {
        this.time = initObj.time
      }
      else {
        this.time = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type objectinfo
    // Serialize message field [who]
    bufferOffset = _serializer.string(obj.who, buffer, bufferOffset);
    // Serialize message field [time]
    bufferOffset = _serializer.int32(obj.time, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type objectinfo
    let len;
    let data = new objectinfo(null);
    // Deserialize message field [who]
    data.who = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [time]
    data.time = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.who.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'ros_counteruav/objectinfo';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '59a9b469fbe19b4315bbcb0d3d4775aa';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string who
    int32 time
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new objectinfo(null);
    if (msg.who !== undefined) {
      resolved.who = msg.who;
    }
    else {
      resolved.who = ''
    }

    if (msg.time !== undefined) {
      resolved.time = msg.time;
    }
    else {
      resolved.time = 0
    }

    return resolved;
    }
};

module.exports = objectinfo;
